import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, takeUntil } from "rxjs";
import { Usuario } from "../models/usuario.models";
import { Cola } from "../models/cola.models";
import { Escritorio } from "../models/escritorio.models";
import { Ticket } from "../models/tickets.models";

@Injectable({
  providedIn: "root"
})
export class apiService{
    private ApiUrl = "http://127.0.0.1:8000/api/";
    private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
    };
    constructor (private http:HttpClient ){}

    public getUsuario():Observable<Usuario[]>{
        return this.http.get<Usuario[]>(this.ApiUrl+'usuarios/');
    }

    public postUsuario(usuario:Usuario): Observable<Usuario>{
    let body = JSON.stringify(usuario);
    return this.http.post<Usuario>(this.ApiUrl+'usuarios/',body,this.httpOptions);
    }
    public putUsuario(usuario:Usuario): Observable<Usuario>{
    let body = JSON.stringify(usuario);
    return this.http.put<Usuario>(this.ApiUrl+'usuarios/'+usuario.id+"/",body,this.httpOptions);
    }
    public deleteUsuario(id:string):Observable<void>{
        return this.http.delete<void>(this.ApiUrl+'usuarios/'+id+"/");
    }
    public getColas():Observable<Cola[]>{
      return this.http.get<Cola[]>(this.ApiUrl+'colas/');
    }

    public postColas(cola:Cola):Observable<Cola>{
      let body = JSON.stringify(cola);
      return this.http.post<Cola>(this.ApiUrl+'colas/',body,this.httpOptions);
    }
    public putColas(cola:Cola):Observable<Cola>{
      let body = JSON.stringify(cola);
      return this.http.put<Cola>(this.ApiUrl+'colas/'+cola.id+"/",body,this.httpOptions);
    }
    public deleteColas(id:string):Observable<void>{
        return this.http.delete<void>(this.ApiUrl+'colas/'+id+"/");
    }
    public getDesk():Observable<Escritorio[]>{
      return this.http.get<Escritorio[]>(this.ApiUrl+'escritorios/')
    }
    public postDesk(escritorio:Escritorio):Observable<Escritorio>{
      let body = JSON.stringify(escritorio);
      return this.http.post<Escritorio>(this.ApiUrl+'escritorios/',body,this.httpOptions);
    }
    public putDesk(escritorio:Escritorio):Observable<Escritorio>{
      let body = JSON.stringify(escritorio);
      return this.http.put<Escritorio>(this.ApiUrl+'escritorios/'+escritorio.id+'/',body,this.httpOptions);
    }
    public deleteDesk(id:string):Observable<void>{
      return this.http.delete<void>(this.ApiUrl+'escritorios/'+id+'/');
    }
    public getTicket():Observable<Ticket[]>{
      return this.http.get<Ticket[]>(this.ApiUrl+'tickets/');
    }
    public postTicket(ticket:Ticket):Observable<Ticket>{
      let body = JSON.stringify(ticket);
      return this.http.post<Ticket>(this.ApiUrl+'tickets/',body,this.httpOptions);
    }
    public putTicket(ticket: Ticket):Observable<Ticket>{
      let body = JSON.stringify(ticket);
      return this.http.put<Ticket>(this.ApiUrl+'tickets/'+ticket.id+'/',body, this.httpOptions);
    }
    public deleteTicket(id:string):Observable<void>{
      return this.http.delete<void>(this.ApiUrl+'tickets/'+id+'/');
    }




}
