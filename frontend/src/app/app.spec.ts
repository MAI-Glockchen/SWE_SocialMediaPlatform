import { describe, it, expect } from 'vitest';
import { App } from './app';

describe('App (pure Vitest)', () => {
  it('should create the app', () => {
    const app = new App();
    expect(app).toBeTruthy();
  });
  
});
