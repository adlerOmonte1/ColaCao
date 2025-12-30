import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { apiService } from '../../../service/api.service';
import { Escritorio } from '../../../models/escritorio.models';
import { Cola } from '../../../models/cola.models';
import { Usuario } from '../../../models/usuario.models';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-desk',
  standalone: true,
  imports: [CommonModule,FormsModule],
  templateUrl: './desk.html',
  styleUrl: './desk.css',
})
export class Desk {
  apiService = inject(apiService);
  cd = inject(ChangeDetectorRef);

  desks : Escritorio[];

/// colas y usuarios

  colas : Cola[];
  colaSeleccionada? : Cola[] =[];

  users: Usuario[];
  usuarioSeleccionado?: Usuario;

  abrirModal:boolean = false;
  textoDialogo:string ;
  objetoDesk : Escritorio = new Escritorio();
  nuevoDesk:boolean = true;


  cerrarModal(){
    this.abrirModal = false;
  }
  ngOnInit(){
    this.obtenerDesk();
    this.obtenerColas();
    this.obtenerUsuarios();
  }
  obtenerDesk(){
    this.apiService.getDesk().subscribe({
      next:(data)=>{

        this.desks= data;
        this.cd.detectChanges();
        console.log("Datos Obtenidos",this.desks);
      }
    })
  }
  obtenerUsuarios(){
    this.apiService.getUsuario().subscribe({
      next:(data)=>{
        this.users = data;
      }
    })
  }
  obtenerColas(){
    this.apiService.getColas().subscribe({
      next:(data)=>{
        this.colas = data;
      }
    })
  }

  crearEscritorio(){
    this.abrirModal = true;
    this.textoDialogo = "Nuevo Escritorio";
    this.objetoDesk = new Escritorio();
    this.colaSeleccionada = undefined;
    this.usuarioSeleccionado = undefined;
  }
  editarEscritorio(escritorio:Escritorio){
    this.abrirModal = true;
    this.nuevoDesk = false;
    this.textoDialogo = "Editar Escritorio";
    this.objetoDesk= escritorio;
    this.usuarioSeleccionado = this.users.find(c=>c.id === escritorio.usuario.id);

    //this.colaSeleccionada = this.colas.find(a =>a.id === escritorio.colas_info.id
    this.colaSeleccionada = [];
    if(escritorio.colas_info && escritorio.colas_info.length>0){
      escritorio.colas_info.forEach(info=>{
        const colaOriginal = this.colas.find(b =>b.id === info.id);
        if(colaOriginal){
          this.colaSeleccionada?.push(colaOriginal);
        }
      });
    }}
    toggleCola(cola: Cola, event?: any) {
    if (event.target.checked) {
      // Si se marcó, agregamos al array
      this.colaSeleccionada?.push(cola);
    } else {
      // Si se desmarcó, lo sacamos del array filtrando por ID
      this.colaSeleccionada = this.colaSeleccionada?.filter(c => c.id !== cola.id);
    }
  }

  // 4. FUNCIÓN AUXILIAR: Para saber si el checkbox debe estar marcado (Visual)
  estaSeleccionada(cola: Cola): boolean {
    return this.colaSeleccionada?.some(c => c.id === cola.id) ?? false;
  }


  guardarEscritorio(){

    const idsColas = this.colaSeleccionada?.map(b => b.id);
    const escritorio:any={
      id:this.objetoDesk.id,
      usuario: this.usuarioSeleccionado?.id,
      numero_ventanilla : this.objetoDesk.numero_ventanilla,
      colas_que_atiende : idsColas

    };
    if (this.nuevoDesk) {
      // POST
      this.apiService.postDesk(escritorio).subscribe({
        next: () => {
          this.cerrarModal();
          this.obtenerDesk(); // Recargar tabla
        },
        error: (e) => console.error(e)
      });
    } else {
      // PUT
      // Asumiendo que tu servicio espera (id, objeto) o (objeto)
      this.apiService.putDesk(escritorio).subscribe({
        next: () => {
          this.cerrarModal();
          this.obtenerDesk(); // Recargar tabla
        },
        error: (e) => console.error(e)
      });
    }
  }
  eliminarEscritorio(id:any){
    if(confirm('Estas Seguro')){
      this.apiService.deleteDesk(id).subscribe(()=>{
        this.obtenerDesk();
        this.cd.detectChanges();

      })
    }
  }
}



