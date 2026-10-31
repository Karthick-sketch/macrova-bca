import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../../environments/environment';

export const BaseUrlPrefixInterceptor: HttpInterceptorFn = (req, next) => {
  const baseUrl = environment.baseUrl;
  if (!req.url.startsWith('http')) {
    const cloneReq = req.clone({ url: `${baseUrl}${req.url}` });
    return next(cloneReq);
  }
  return next(req);
};
