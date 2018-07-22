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

export async function searchURLs(token, search, offset=0, limit=100) {
    const result = await apiCall(
        token, 
        'GET', 
        '/_/api/v1/url',
        {
            search: search,
            offset: offset,
            limit: limit,
        }
    );

    result.data.forEach(row => row.views = row.stats.reduce((a, b) => a + b.count, 0));

    return {
        rows: result.data,
        hasMore: result.data.length >= limit,
    };
}

export async function createURL(token, urlObject) {
    return await apiCall(
        token,
        'POST',
        '/_/api/v1/url',
        null,
        urlObject
    );
}

export async function updateURL(token, urlObject) {
    return await apiCall(
        token,
        'PUT',
        `/_/api/v1/url/${urlObject.id}`,
        null,
        urlObject
    );
}

export async function getURL(token, urlId) {
    const result = await apiCall(
        token,
        'GET',
        `/_/api/v1/url/${urlId}`,
    );

    result.data.views = result.data.stats.reduce((a, b) => a + b.count, 0);

    return result;
}

export async function getURLLogs(token, urlId) {
    return await apiCall(
        token,
        'GET',
        `/_/api/v1/url/${urlId}/logs`,
    );
}