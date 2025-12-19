import { Component } from '@angular/core';
import {Router} from '@angular/router'
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../../service/auth.service';
@Component({
  selector: 'app-login',
  imports: [FormsModule, CommonModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  // varialbes que se guardara lo q el usuario escriba
  email: string = '';
  password : string = '';

  constructor(private router:Router, private authService:AuthService ){}

  onLogin(){
    if (!this.email || !this.password) {
        alert('Por favor, completa todos los campos.');
        return;
    }
    this.authService.login(this.email,this.password).subscribe(
      {
        next:(response)=>{
          console.log('Exitoso');
          this.router.navigate(['usuarios']);
        },
        error: (error) =>{
          console.log('error en el login',error);
          if(error.status==400){
            alert('Correo o contraseña incorrecta');
          }else if(error.status==0){
            alert('No hay conexion con el servidor');
          }else {
            alert('Ocurrio un error inesperado');
          }
        }
      }
    )
  }
}
