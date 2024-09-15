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
import EditTeam from '../components/relay/EditTeam.vue';

import ConfirmationComponent from '../components/registration/ConfirmationComponent.vue';
import AboutComponent from '../components/AboutComponent.vue';
import ContactComponent from '../components/ContactComponent.vue';
import PrivacyPolicy from '../components/PrivacyPolicy.vue';
import TermsOfAgreement from '../components/TermsOfAgreement.vue';
import LoginComponent from '../components/LoginComponent.vue';
import DashboardComponent from '../components/dashboard/DashboardComponent.vue';
import CreateEvent from '../components/dashboard/CreateEvent.vue';


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
  {
    path: '/events/:eventUrlAlias/team-results',
    name: 'TeamResultsParent',
    component: TeamResultsParent,
  },
  {
    path: '/events/:eventUrlAlias/team-results/:raceId',
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
    path: '/edit-team/:token',
    name: 'EditTeam',
    component: EditTeam
  },
  {
    path: '/events/:url_alias/register',
    name: 'RegisterAndWaiver',
    component: RegisterAndWaiver,
    props: true
  },
  {
    path: '/privacy-policy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy,
  },
  {
    path: '/terms-of-agreement',
    name: 'TermsOfAgreement',
    component: TermsOfAgreement,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginComponent,
  },
  {
    path: '/dashboard',
    name: 'DashboardComponent',
    component: DashboardComponent,
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard/create-event',
    name: 'CreateEvent',
    component: CreateEvent,
    meta: { requiresAuth: true },
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

// Navigation guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('access_token');
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
});

export default router;
