// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import PricingComponent from '../components/PricingComponent.vue';
import EventComponent from '../components/EventComponent.vue';
import RaceRegistrationComponent from '@/components/RaceRegistrationComponent.vue';

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
    name: 'RaceRegistrationComponent',
    component: RaceRegistrationComponent,
    props: true
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
