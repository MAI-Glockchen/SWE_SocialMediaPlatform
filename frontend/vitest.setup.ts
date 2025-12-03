// Load Zone.js first (required for zone-testing to patch async APIs)
import 'zone.js';

// Then load Angular's zone-testing bundle
import 'zone.js/testing';

import { TestBed } from '@angular/core/testing';
import {
  BrowserTestingModule,
  platformBrowserTesting
} from '@angular/platform-browser/testing';

// Initialize Angular's testing environment
TestBed.initTestEnvironment(
  BrowserTestingModule,
  platformBrowserTesting()
);
