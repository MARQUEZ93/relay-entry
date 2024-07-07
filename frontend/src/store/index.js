import { createStore } from 'vuex';
// TODO: null check this entire shit
const store = createStore({
  state() {
    return {
      registrationData: null,
      raceData: null,
      teamData: null,
      paymentData: null,
    };
  },
  mutations: {
    setConfirmationData(state, data) {
      state.registrationData = data.registrationData;
      state.teamData = data.teamData;
      state.raceData = data.raceData;
      state.paymentData = data.paymentData;
    },
    clearConfirmationData(state) {
      state.registrationData = null;
      state.raceData = null;
      state.teamData = null;
      state.paymentData = null;
    },
  },
});

export default store;
