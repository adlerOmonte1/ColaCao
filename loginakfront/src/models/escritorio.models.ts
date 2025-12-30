import { ColaInfo } from "./colas_info.models";
import { Usuario } from "./usuario.models";

export class Escritorio{
  id: string;
  usuario:Usuario;
  numero_ventanilla: string;
  colas_que_atiende: number[];
  colas_info : ColaInfo[];
}

