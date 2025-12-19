import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { tap } from 'rxjs';
import { email } from '@angular/forms/signals';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private loginUrl = 'http://127.0.0.1:8000/api/auth/login/';

  constructor(private http: HttpClient) {}

  login(email: string, password: string) {
    return this.http.post<any>(this.loginUrl, { email, password }).pipe(
      tap(res=>{
        console.log('Respuesta del servidor:',res)
        localStorage.setItem('refresh',res.refresh)
        localStorage.setItem('token',res.access)
        localStorage.setItem('user_id',res.user_id)
        localStorage.setItem('rol',res.rol)
        //localStorage.setItem('rol',res.usuario.rol.toUpperCase()); // toUpperCase() para que la comparacion sea entre mayusculas
        //localStorage.setItem('userId', res.usuario.id); // para guardar el ID del usuario del uso del carrito
      })
    );
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('token')
    return !!token;
  }
}
