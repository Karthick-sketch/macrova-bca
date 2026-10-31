import { Component, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { UserSignupDTO } from '../dto/user-signup.dto';
import { AuthService } from '../auth.service';
import { ToastComponent } from '../../toast/toast.component';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  imports: [FormsModule, RouterLink, ToastComponent],
  styleUrl: './signup.component.css',
})
export class SignupComponent implements OnInit {
  @ViewChild(ToastComponent) toast!: ToastComponent;

  user: UserSignupDTO;

  constructor(
    private authService: AuthService,
    private router: Router,
  ) {
    this.user = new UserSignupDTO();
  }

  ngOnInit(): void {
    this.authService.isAuthenticated().subscribe((isAuth) => {
      if (isAuth) {
        this.router.navigate(['/dashboard']);
      }
    });
  }

  submit() {
    if (this.validateUserDetails()) {
      this.authService.signup(this.user).subscribe(() => {
        this.router.navigate(['/dashboard']);
      });
    }
  }

  private validateUserDetails() {
    // username validation
    if (!this.user.username) {
      this.toast.showError('Username is empty');
      return false;
    } else if (this.user.username.length < 3) {
      this.toast.showError('Username must be at least 3 characters long');
      return false;
    } else if (this.user.username.length > 20) {
      this.toast.showError('Username must be at most 20 characters long');
      return false;
    } else if (!this.user.username.match(/^[a-zA-Z0-9]+$/)) {
      this.toast.showError('Username must contain only letters and numbers');
      return false;
    } else if (/^[0-9]/.test(this.user.username)) {
      this.toast.showError('Username must not start with a number');
      return false;
    }

    // email validation
    if (!this.user.email) {
      this.toast.showError('Email is empty');
      return false;
    } else if (
      !this.user.email.match(/^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$/)
    ) {
      this.toast.showError('Email is invalid');
      return false;
    }

    // password validation
    if (!this.user.password) {
      this.toast.showError('Password is empty');
      return false;
    } else if (this.user.password.length < 8) {
      this.toast.showError('Password must be at least 8 characters long');
      return false;
    } else if (!this.user.password.match(/^[a-zA-Z0-9]+$/)) {
      this.toast.showError('Password must contain only letters and numbers');
      return false;
    } else if (this.user.password.length > 20) {
      this.toast.showError('Password must be at most 20 characters long');
      return false;
    }

    return true;
  }
}
