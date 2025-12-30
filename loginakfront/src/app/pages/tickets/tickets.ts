import { CommonModule } from '@angular/common';
import { ChangeDetectorRef, Component, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { apiService } from '../../../service/api.service';
import { Ticket } from '../../../models/tickets.models';

@Component({
  selector: 'app-tickets',
  standalone:true,
  imports: [CommonModule, FormsModule],
  templateUrl: './tickets.html',
  styleUrl: './tickets.css',
})
export class Tickets {

  apiService = inject(apiService);
  cd = inject(ChangeDetectorRef);

  tickets : Ticket[];

  obtenerTicket(){
    this.apiService.getTicket().subscribe({
      next:(data)=>{
        this.tickets = data;
        this.cd.detectChanges();
        console.log('Datos recibidos:',this.tickets);
      }
    })
  }
  ngOnInit(){
    this.obtenerTicket();
  }


}
