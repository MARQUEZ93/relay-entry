import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    iconfont: 'mdi', // Ensure you are using 'mdi' for Material Design Icons
  },
});

export default vuetify;
