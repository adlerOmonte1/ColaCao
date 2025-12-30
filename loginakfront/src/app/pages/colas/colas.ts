import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core'; // <--- 1. Importar ChangeDetectorRef
import { apiService } from '../../../service/api.service';
import { Cola } from '../../../models/cola.models';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-colas',
  standalone:true,
  imports: [CommonModule,FormsModule],
  templateUrl: './colas.html',
  styleUrl: './colas.css',
})
export class Colas implements OnInit{
  apiservice = inject(apiService);
  cd = inject(ChangeDetectorRef); // <--- 2. Inyectarlo aquí
  colas : Cola[];

  // Crear nueva cola
  tituloDialogo: string = 'Nueva Ventanilla';
  nuevaCola: boolean = true;
  objetoCola: Cola = new Cola();

  // Logica de abrir dialogo
  abrirModal:boolean = false;


  ngOnInit(){
    this.ObtenerColas();
    console.log(this.colas);
  }

  ObtenerColas(){
    this.apiservice.getColas().subscribe({
      next: (data)=>{
        console.log('✅ Datos recibidos:', data);
        this.colas=data;
        this.cd.detectChanges();
      },
    }
    )
  }
  eliminar(id:any){
    if(confirm('Estas seguro')){
      this.apiservice.deleteColas(id).subscribe(()=> {
        this.ObtenerColas();
        this.cd.detectChanges();
      })
    }
  }
  crearCola(){
    this.abrirModal = true;
    this.nuevaCola = true;
    this.objetoCola = new Cola();
  }

  editarCola(cola:Cola){
    this.abrirModal = true;
    this.tituloDialogo = "Editar Ventanilla";
    this.objetoCola = cola; //obtiene el objeto, para editar
    this.nuevaCola = false;
  }
  cerrarModal(){
    this.abrirModal = false;
    this.ObtenerColas();
  }
  guardarCambios(){
    if(this.nuevaCola){
      this.apiservice.postColas(this.objetoCola).subscribe({
        next:()=>{
          this.ObtenerColas();
          this.cerrarModal();
          console.log("Objeto creado")
        }
      })
    } else {
      this.apiservice.putColas(this.objetoCola).subscribe({
        next:()=>{
          this.ObtenerColas();
          this.cerrarModal();
          console.log("Objeto editado")
        }
      })
    }
  }




}


