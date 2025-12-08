import { ApplicationConfig, importProvidersFrom } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { NgIconsModule } from '@ng-icons/core';
import {
  heroTrash
} from '@ng-icons/heroicons/outline';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),

    importProvidersFrom(
      NgIconsModule.withIcons({
        heroTrash
      })
    )
  ],
};
