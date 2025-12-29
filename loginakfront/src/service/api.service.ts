import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Observable, takeUntil } from "rxjs";
import { Usuario } from "../models/usuario.models";
import { Cola } from "../models/cola.models";

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
      return this.http.post<Cola>(this.ApiUrl+'colas/'+cola.id+"/",body,this.httpOptions);
    }
    public deleteColas(id:string):Observable<void>{
        return this.http.delete<void>(this.ApiUrl+'colas/'+id+"/");
    }

}
