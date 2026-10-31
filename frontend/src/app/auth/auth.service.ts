import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, Observable, of, tap } from 'rxjs';
import { TokenService } from './token.service';
import { UserSignupDTO } from './dto/user-signup.dto';
import { UserLoginDTO } from './dto/user-login.dto';
import { UsernameDTO } from './dto/username.dto';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  username = signal<string | null>(null);

  private accessToken: string | null = null;

  constructor(
    private http: HttpClient,
    private tokenService: TokenService,
  ) {}

  setAccessToken(token: string) {
    this.accessToken = token.replace('Bearer ', '');
  }

  getAccessToken() {
    return this.accessToken;
  }

  hasAccessToken() {
    return !!this.accessToken;
  }

  clearAccessToken() {
    this.accessToken = null;
  }

  signup(userSignupDTO: UserSignupDTO) {
    return this.http
      .post('/user/register', userSignupDTO)
      .pipe(tap(() => this.fetchUsername()));
  }

  login(userLoginDTO: UserLoginDTO) {
    return this.http
      .post('/authenticate', userLoginDTO, {
        withCredentials: true,
      })
      .pipe(tap(() => this.fetchUsername()));
  }

  logout() {
    return this.http
      .post('/user/logout', {}, { withCredentials: true })
      .pipe(tap(() => this.username.set(null)));
  }

  requestRefreshToken() {
    return this.http.post(
      '/user/refresh',
      {},
      {
        withCredentials: true,
        observe: 'response',
      },
    );
  }

  isAuthenticated(): Observable<boolean> {
    if (this.tokenService.isLoggedIn(this.accessToken)) {
      return of(true);
    }

    return this.requestRefreshToken().pipe(
      map((res: any) => {
        const accessToken = res.body?.accessToken;
        if (accessToken) {
          this.setAccessToken(accessToken);
          this.fetchUsername();
          return true;
        }
        return false;
      }),
      catchError(() => {
        this.clearAccessToken();
        return of(false);
      }),
    );
  }

  getUsername() {
    return this.http.get<UsernameDTO>('/user/username');
  }

  private fetchUsername() {
    this.getUsername().subscribe({
      next: ({ username }) => this.username.set(username),
      error: () => this.username.set(null),
    });
  }
}
