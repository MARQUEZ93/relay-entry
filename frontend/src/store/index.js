import { createStore } from 'vuex';
// TODO: null check this entire shit
const store = createStore({
  state() {
    return {
      confirmationCode: null,
      registrationData: null,
      raceData: null,
      teamData: null,
      paymentAmount: null,
      paymentStatus: null,
    };
  },
  mutations: {
    setConfirmationData(state, data) {
      state.confirmationCode = data.confirmationCode;
      state.registrationData = data.registrationData;
      state.teamData = data.teamData;
      state.raceData = data.raceData;
      state.paymentStatus = data.paymentStatus;
      state.paymentAmount = data.paymentAmount;
    },
    clearConfirmationData(state) {
      state.confirmationCode = null;
      state.registrationData = null;
      state.raceData = null;
      state.teamData = null;
      state.paymentStatus = null;
      state.paymentAmount = null;
    },
  },
});

export default store;
