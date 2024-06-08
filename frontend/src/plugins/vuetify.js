import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
  // theme: {
  //   themes: {
  //     light: {
  //       primary: '#2ecc71', // Emerald Green as the primary color
  //       secondary: '#4caf50', // Optional: Define a secondary color
  //     },
  //   },
  // }
});

export default vuetify;
