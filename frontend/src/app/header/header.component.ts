import { Component, ElementRef, OnDestroy, OnInit, computed } from '@angular/core';
import { NavigationEnd, Router, RouterLink } from '@angular/router';
import { filter } from 'rxjs';
import { AuthService } from '../auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.css',
  imports: [RouterLink],
})
export class HeaderComponent implements OnInit, OnDestroy {
  initial = computed(() => {
    // Read the signal once to avoid reading it twice — if read separately for
    // the check and .charAt(), the value could change between reads (e.g. null
    // to string during initial load), causing .toUpperCase() to fail on undefined.
    const username = this.authService.username();
    return username ? username.charAt(0).toUpperCase() : 'K';
  });

  isLogin = false;
  isSignup = false;
  isProfileExpanded = false;
  endpoints = ['dashboard', 'progress', 'meals', 'history'];
  endpoint = 'dashboard';

  private outsideClickListener = (event: MouseEvent) => {
    const profileIcon = this.elementRef.nativeElement.querySelector('.profile-icon');
    if (!profileIcon?.contains(event.target as Node)) {
      this.isProfileExpanded = false;
      this.removeOutsideClickListener();
    }
  };

  constructor(
    private router: Router,
    private authService: AuthService,
    private elementRef: ElementRef,
  ) {}

  ngOnDestroy() {
    this.removeOutsideClickListener();
  }

  ngOnInit() {
    this.router.events
      .pipe(filter((event) => event instanceof NavigationEnd))
      .subscribe((event: NavigationEnd) => {
        this.isLogin = event.url === '/login';
        this.isSignup = event.url === '/signup';
        this.endpoint = event.url.slice(1);
      });
  }

  isActive(endpoint: string) {
    return this.endpoint === endpoint;
  }

  expandProfile() {
    this.isProfileExpanded = !this.isProfileExpanded;
    if (this.isProfileExpanded) {
      this.addOutsideClickListener();
    } else {
      this.removeOutsideClickListener();
    }
  }

  private addOutsideClickListener() {
    document.addEventListener('click', this.outsideClickListener);
  }

  private removeOutsideClickListener() {
    document.removeEventListener('click', this.outsideClickListener);
  }

  signOut() {
    this.authService.logout().subscribe(() => {
      this.authService.clearAccessToken();
      this.router.navigate(['/login']);
    });
  }
}
