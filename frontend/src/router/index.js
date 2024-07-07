// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import PricingComponent from '../components/PricingComponent.vue';
import EventComponent from '../components/EventComponent.vue';
import NotFound from '../components/NotFound.vue';
import RegistrationView from '../components/registration/RegistrationView.vue';
import ConfirmationComponent from '../components/registration/ConfirmationComponent.vue';
import store from '@/store'; // Import the store
const routes = [
  {
    path: '/',
    name: 'HomeComponent',
    component: HomeComponent,
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
    path: '/events/:url_alias/:id',
    name: 'RegistrationView',
    component: RegistrationView,
    props: true
  },
  {
    path: '/confirmation',
    name: 'Confirmation',
    component: ConfirmationComponent,
    props: true,
    beforeEnter: (to, from, next) => {
      // TODO: waiver vs payment forms 
      if (!store.state.registrationData || !store.state.raceData) {
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
  scrollBehavior() {
    console.log("scrolled");
    return { x: 0, y: 0 };
  },
});

export default router;
