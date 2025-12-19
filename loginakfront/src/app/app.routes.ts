import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Register } from './pages/register/register';
import { Dashboard } from './pages/dashboard/dashboard';
import { User } from './pages/user/user';

export const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch:'full'},

  {path:'login', component:Login},
  {path:'register', component:Register},
  {path:'dashboard', component:Dashboard},
  {path:'usuarios',component:User},
  {path:'**', redirectTo:'login'}

];
