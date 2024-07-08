import { createStore } from 'vuex';
const store = createStore({
  state() {
    return {
      registrationData: null,
      raceData: null,
      teamData: null,
      paymentData: null,
      eventData: null
    };
  },
  mutations: {
    setConfirmationData(state, data) {
      state.paymentData = data.paymentData;
      state.registrationData = data.registrationData;
      state.teamData = data.teamData;
      state.raceData = data.raceData;
      state.eventData = data.eventData;
    },
    clearConfirmationData(state) {
      state.registrationData = null;
      state.teamData = null;
      state.paymentData = null;
      state.raceData = null;
      state.eventData = null;
    },
  },
});

export default store;
