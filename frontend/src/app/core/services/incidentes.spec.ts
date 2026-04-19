import { TestBed } from '@angular/core/testing';

import { Incidentes } from './incidentes';

describe('Incidentes', () => {
  let service: Incidentes;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Incidentes);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
