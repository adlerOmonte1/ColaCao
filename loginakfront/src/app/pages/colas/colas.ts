import { CommonModule } from '@angular/common';
import { Component, inject, OnInit, ChangeDetectorRef } from '@angular/core'; // <--- 1. Importar ChangeDetectorRef
import { apiService } from '../../../service/api.service';
import { Cola } from '../../../models/cola.models';

@Component({
  selector: 'app-colas',
  standalone:true,
  imports: [CommonModule],
  templateUrl: './colas.html',
  styleUrl: './colas.css',
})
export class Colas implements OnInit{
  apiservice = inject(apiService);
  cd = inject(ChangeDetectorRef); // <--- 2. Inyectarlo aquí
  colas : Cola[];

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

}


