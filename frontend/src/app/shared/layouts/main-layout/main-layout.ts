import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { SidebarComponent } from '../../components/sidebar/sidebar';

@Component({
  selector: 'app-main-layout',
  standalone: true,
  imports: [CommonModule, RouterOutlet, SidebarComponent],
  template: `
    <div class="layout-container">
      <app-sidebar></app-sidebar> <main class="main-content">
        <router-outlet></router-outlet> </main>
    </div>
  `,
  styles: [`
    .layout-container {
      display: flex;
      height: 100vh;
      width: 100vw;
      overflow: hidden;
    }
    .main-content {
      flex: 1;
      overflow-y: auto;
      background-color: #f4f7f6;
      padding: 20px;
    }
  `]
})
export class MainLayoutComponent {}