import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { DashboardComponent } from './features/dashboard/dashboard';
import { MainLayoutComponent } from './shared/layouts/main-layout/main-layout';
import { BitacoraComponent } from './features/bitacora/bitacora';
import { RegistroTallerComponent } from './components/registro-taller/registro-taller';
import { LandingComponent } from './components/landing/landing';
export const routes: Routes = [
  { path: '', component: LandingComponent },


  { path: 'login', component: LoginComponent },
  { path: 'registro-taller', component: RegistroTallerComponent },
  
  // Agrupamos las rutas que llevan el Sidebar
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      { path: 'dashboard', component: DashboardComponent },
      { path: 'bitacora', component: BitacoraComponent },
      // Aquí agregarás los CRUDs: { path: 'vehiculos', component: VehiculosComponent }
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  },

  { path: '**', redirectTo: '/login',}
];