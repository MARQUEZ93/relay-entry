import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      confirmationCode: null,
      registrationData: null,
      raceData: null,
      paymentIntent: null,
    };
  },
  mutations: {
    setConfirmationData(state, data) {
      state.confirmationCode = data.confirmationCode;
      state.registrationData = data.registrationData;
      state.raceData = data.raceData;
      state.paymentIntent = data.paymentIntent;
    },
    clearConfirmationData(state) {
      state.confirmationCode = null;
      state.registrationData = null;
      state.raceData = null;
      state.paymentIntent = null;
    },
  },
});

export default store;
