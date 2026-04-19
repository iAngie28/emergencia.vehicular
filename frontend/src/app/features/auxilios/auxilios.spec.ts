import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Auxilios } from './auxilios';

describe('Auxilios', () => {
  let component: Auxilios;
  let fixture: ComponentFixture<Auxilios>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Auxilios],
    }).compileComponents();

    fixture = TestBed.createComponent(Auxilios);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
