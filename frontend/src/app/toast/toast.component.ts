import { Component } from '@angular/core';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrl: './toast.component.css',
})
export class ToastComponent {
  message = '';

  showError(errorMessage: string) {
    this.message = errorMessage;
    setTimeout(() => {
      this.message = '';
    }, 5000);
  }
}
