import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';

export interface JwtPayload {
  exp: number;
  iat?: number;
  sub?: string;

  [key: string]: any;
}

@Injectable({
  providedIn: 'root',
})
export class TokenService {
  isLoggedIn(accessToken: string | null): boolean {
    if (!accessToken) {
      return false;
    }
    return !this.isTokenExpired(accessToken);
  }

  private isTokenExpired(accessToken: string): boolean {
    const payload = this.decodeToken(accessToken);
    if (!payload) return true;
    const now = Math.floor(Date.now() / 1000);
    return payload.exp < now;
  }

  private decodeToken(accessToken: string): JwtPayload | null {
    try {
      return jwtDecode<JwtPayload>(accessToken);
    } catch (e) {
      return null;
    }
  }
}
