import { Routes } from '@angular/router';
import { LoginComponent } from './features/auth/login/login';
import { DashboardComponent } from './features/dashboard/dashboard';
import { MainLayoutComponent } from './shared/layouts/main-layout/main-layout';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },
  
  // Agrupamos las rutas que llevan el Sidebar
  {
    path: '',
    component: MainLayoutComponent,
    children: [
      { path: 'dashboard', component: DashboardComponent },
      // Aquí agregarás los CRUDs: { path: 'vehiculos', component: VehiculosComponent }
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' }
    ]
  },

  { path: '**', redirectTo: '/login' }
];