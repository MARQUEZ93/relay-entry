const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    }
  },
  transpileDependencies: [
    'vuetify',
  ],
  devServer: {
    hot: true,
    liveReload: true,
    watchFiles: ['src/**/*', 'public/**/*'],
    port: process.env.VUE_APP_PORT,
    host: '0.0.0.0',
    client: {
      webSocketURL: process.env.VUE_APP_WEBSOCKET_URL,
      overlay: {
        warnings: false,
        errors: true,
      },
      progress: true,
    },
  },
  // Explicitly set the output directory to dist
  outputDir: 'dist',
});
