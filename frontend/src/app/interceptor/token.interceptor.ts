import { inject } from '@angular/core';
import { HttpInterceptorFn } from '@angular/common/http';
import { switchMap } from 'rxjs';
import { AuthService } from '../auth/auth.service';

const PUBLIC_URLS = ['/authenticate', '/user/register', '/user/refresh'];

export const TokenInterceptor: HttpInterceptorFn = (req, next) => {
  if (PUBLIC_URLS.some((url) => req.url.includes(url))) {
    return next(req);
  }

  const authService = inject(AuthService);

  return authService.isAuthenticated().pipe(
    switchMap((isAuth) => {
      if (isAuth) {
        const token = authService.getAccessToken();
        const cloneReq = req.clone({
          setHeaders: { Authorization: `Bearer ${token}` },
          withCredentials: true,
        });
        return next(cloneReq);
      }
      return next(req);
    }),
  );
};
