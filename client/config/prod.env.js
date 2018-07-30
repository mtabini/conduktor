'use strict'

module.exports = {
  NODE_ENV: '"production"',
  API_URL: JSON.stringify(process.env.API_URL || 'http://localhost:3000'),
  AUTHORIZED_DOMAINS: JSON.stringify(process.env.AUTHORIZED_DOMAINS),
  GOOGLE_OAUTH_CLIENT_ID: JSON.stringify(process.env.GOOGLE_OAUTH_CLIENT_ID),
  APP_TITLE: JSON.stringify(process.env.APP_TITLE || 'Conduktor'),
  BASE_URL: JSON.stringify(process.env.BASE_URL || 'Conduktor'),
}
