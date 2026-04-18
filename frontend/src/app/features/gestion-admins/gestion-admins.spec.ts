import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionAdmins } from './gestion-admins';

describe('GestionAdmins', () => {
  let component: GestionAdmins;
  let fixture: ComponentFixture<GestionAdmins>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionAdmins],
    }).compileComponents();

    fixture = TestBed.createComponent(GestionAdmins);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
