import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { DashboardComponent } from './features/dashboard/dashboard';
import { MainLayoutComponent } from './shared/layouts/main-layout/main-layout';
import { BitacoraComponent } from './features/bitacora/bitacora';
import { RegistroTallerComponent } from './components/registro-taller/registro-taller';
import { LandingComponent } from './components/landing/landing';
import { GestionAdminsComponent } from './features/gestion-admins/gestion-admins';
import { ForgotPasswordComponent } from './features/auth/forgot-password/forgot-password';
import { ResetPasswordComponent } from './features/auth/reset-password/reset-password';

export const routes: Routes = [
  { path: '', component: LandingComponent },


  { path: 'login', component: LoginComponent },
  { path: 'forgot-password', component: ForgotPasswordComponent },
  { path: 'reset-password', component: ResetPasswordComponent },
  { path: 'registro-taller', component: RegistroTallerComponent },
  
  // Agrupamos las rutas que llevan el Sidebar
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      { path: 'dashboard', component: DashboardComponent },
      { path: 'bitacora', component: BitacoraComponent },
      { path: 'administradores', component: GestionAdminsComponent },
      // Aquí agregarás los CRUDs: { path: 'vehiculos', component: VehiculosComponent }
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  },

  { path: '**', redirectTo: '/login',}
];