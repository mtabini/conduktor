'use strict'

module.exports = {
  NODE_ENV: '"production"',
  API_URL: JSON.stringify(process.env.CONDUKTOR_API_URL || 'http://localhost:3000'),
  AUTHORIZED_DOMAINS: JSON.stringify(process.env.CONDUKTOR_AUTHORIZED_DOMAINS),
  GOOGLE_OAUTH_CLIENT_ID: JSON.stringify(process.env.CONDUKTOR_GOOGLE_OAUTH_CLIENT_ID),
  APP_TITLE: JSON.stringify(process.env.CONDUKTOR_APP_NAME || 'Conduktor'),
}
