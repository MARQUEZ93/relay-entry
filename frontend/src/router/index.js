// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import PricingComponent from '../components/PricingComponent.vue';
import EventComponent from '../components/EventComponent.vue';
import NotFound from '../components/NotFound.vue';
import RegistrationView from '../components/registration/RegistrationView.vue';
import RegisterAndWaiver from '../components/registration/RegisterAndWaiver.vue';
import RegisteredTeams from '../components/relay/RegisteredTeams.vue';
import TeamResultsParent from '../components/relay/TeamResultsParent.vue';
import TeamRaceResults from '../components/relay/TeamRaceResults.vue';

import ConfirmationComponent from '../components/registration/ConfirmationComponent.vue';
import AboutComponent from '../components/AboutComponent.vue';
import ContactComponent from '../components/ContactComponent.vue';
import store from '@/store'; // Import the store
const routes = [
  {
    path: '/',
    name: 'HomeComponent',
    component: HomeComponent,
  },
  {
    path: '/about',
    name: 'AboutComponent',
    component: AboutComponent,
  },
  {
    path: '/contact',
    name: 'ContactComponent',
    component: ContactComponent,
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: PricingComponent,
  },
  {
    path: '/events/:eventUrlAlias',
    name: 'Event',
    component: EventComponent,
  },
  // TODO: null check this for non relay races
  {
    path: '/events/:eventUrlAlias/results',
    name: 'TeamResultsParent',
    component: TeamResultsParent,
  },
  {
    path: '/events/:eventUrlAlias/results/:raceId',
    name: 'TeamRaceResults',
    component: TeamRaceResults,
  },
  {
    path: '/events/:eventUrlAlias/teams',
    name: 'RegisteredTeams',
    component: RegisteredTeams,
  },
  {
    path: '/events/:url_alias/:id',
    name: 'RegistrationView',
    component: RegistrationView,
    props: true
  },
  {
    path: '/events/:url_alias/register',
    name: 'RegisterAndWaiver',
    component: RegisterAndWaiver,
    props: true
  },
  {
    path: '/confirmation',
    name: 'Confirmation',
    component: ConfirmationComponent,
    props: true,
    beforeEnter: (to, from, next) => {
      if (!store.state.registrationData) {
        next('/');
      } else {
        next();
      }
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
