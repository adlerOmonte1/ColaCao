import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Register } from './pages/register/register';
import { Dashboard } from './pages/dashboard/dashboard';
import { User } from './pages/user/user';
import { Colas } from './pages/colas/colas';
import { Desk } from './pages/desk/desk';
import { Tickets } from './pages/tickets/tickets';

export const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch:'full'},

  {path:'login', component:Login},
  {path:'register', component:Register},
  {path:'dashboard', component:Dashboard},
  {path:'usuarios',component:User},
  {path:'colas',component:Colas},
  {path:'desk',component:Desk},
  {path:'tickets/pantalla', component:Tickets},
  {path:'**', redirectTo:'login'}

];
