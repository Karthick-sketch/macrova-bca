import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';
import { UserLoginDTO } from '../dto/user-login.dto';
import { ToastComponent } from '../../toast/toast.component';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  imports: [RouterLink, FormsModule, ToastComponent],
})
export class LoginComponent implements OnInit {
  @ViewChild(ToastComponent) toast!: ToastComponent;

  user: UserLoginDTO;
  isInvalidCredentials = false;

  constructor(
    private authService: AuthService,
    private router: Router,
  ) {
    this.user = new UserLoginDTO();
  }

  ngOnInit(): void {
    this.authService.isAuthenticated().subscribe((isAuth) => {
      if (isAuth) {
        this.router.navigate(['/dashboard']);
      }
    });
  }

  submit() {
    if (this.user.username && this.user.password) {
      this.authService.login(this.user).subscribe({
        next: () => {
          this.router.navigate(['/dashboard']);
        },
        error: () => {
          this.toast.showError('Invalid username or password!');
        },
      });
    }
  }
}
