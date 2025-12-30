import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core'; // <--- 1. Importar ChangeDetectorRef
import { apiService } from '../../../service/api.service';
import { Usuario } from '../../../models/usuario.models';

@Component({
  selector: 'app-user',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './user.html',
  styleUrl: './user.css',
})
export class User implements OnInit {
  apiservice = inject(apiService);
  cd = inject(ChangeDetectorRef); // <--- 2. Inyectarlo aquí

  usuarios : Usuario[]=[];

  ngOnInit(){
    this.getUsuarios();
  }

  getUsuarios(){
    this.apiservice.getUsuario().subscribe({
      next: (data) => {
        console.log('✅ Datos recibidos:', data);
        this.usuarios = data;

        // 3. ¡LA CURITA! Obliga a Angular a pintar la pantalla
        this.cd.detectChanges();
      },
      error: (e) => console.error(e)
    });
  }

  eliminar(id:any){
    if(confirm('Estas seguro')){
      this.apiservice.deleteUsuario(id).subscribe(()=> {
        this.getUsuarios();
      })
    }
  }

}
