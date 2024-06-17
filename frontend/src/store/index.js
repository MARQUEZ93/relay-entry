import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      confirmationCode: null,
      racerData: null,
      raceData: null,
      paymentIntent: null,
    };
  },
  mutations: {
    setConfirmationData(state, data) {
      state.confirmationCode = data.confirmationCode;
      state.racerData = data.racerData;
      state.raceData = data.raceData;
      state.paymentIntent = data.paymentIntent;
    },
    clearConfirmationData(state) {
      state.confirmationCode = null;
      state.racerData = null;
      state.raceData = null;
      state.paymentIntent = null;
    },
  },
});

export default store;
