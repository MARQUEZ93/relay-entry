const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    hot: true,
    liveReload: true,
    watchFiles: ['src/**/*', 'public/**/*'],
    port: '8080',
    host: '0.0.0.0',
    client: {
      webSocketURL: 'ws://localhost:8080/ws',
      overlay: {
        warnings: false,
        errors: true,
      },
      progress: true,
    },
  },
});
