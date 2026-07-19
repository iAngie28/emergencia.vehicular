import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { environment } from '../../../environments/environment';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('token');
  const isApiRequest = req.url.startsWith(environment.apiUrl);
  const router = inject(Router);

  let newReq = req;

  if (token && isApiRequest && !req.headers.has('Authorization')) {
    newReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  return next(newReq).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 403) {
        const detail = error.error?.detail;
        if (typeof detail === 'string' && detail.includes('El taller se encuentra inhabilitado')) {
          router.navigate(['/taller-inhabilitado']);
        }
      }
      return throwError(() => error);
    })
  );
};
