'use strict';

import axios from 'axios';
import { stat } from 'fs';

async function apiCall(token, method, url, query=null, body=null) {
    return await axios.request({
        baseURL: process.env.API_URL,
        timeout: 2000,
        method: method,
        url: url,
        headers: {
            Authorization: `Token ${token}`
        },
        params: query,
        data: body,
    });
}

export async function searchURLs(token, search, limit=0, offset=100) {
    const result = await apiCall(
        token, 
        'GET', 
        '/_/api/v1/url',
        {
            search: search,
            limit: limit,
            offset: offset,
        }
    );

    result.data.forEach(row => row.views = row.stats.reduce((a, b) => a + b.count, 0));

    return result.data;
}

export async function createURL(token, urlObject) {
    const result = await apiCall(
        token,
        'POST',
        '/_/api/v1/url',
        null,
        urlObject
    );

    console.log(result);
}