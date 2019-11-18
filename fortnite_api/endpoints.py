from .enums import GameLanguage, MatchMethod, NewsType
from .item import BrCosmetic
from .news import GameModeNews, News
from .shop import BrShop


class SyncCosmeticsEndpoints:

    def __init__(self, client):
        self._client = client

    def _parse_search_parameter(self, **search_parameters):
        parameters = {
            'language': search_parameters.get('language', GameLanguage.ENGLISH).value,
            'searchLanguage': search_parameters.get('search_language', GameLanguage.ENGLISH).value,
            'matchMethod': search_parameters.get('match_method', MatchMethod.FULL).value
        }
        if search_parameters.__contains__('type'):
            parameters['type'] = search_parameters['type']
        if search_parameters.__contains__('backend_type'):
            parameters['backendType'] = search_parameters['backend_type']
        if search_parameters.__contains__('rarity'):
            parameters['rarity'] = search_parameters['rarity']
        if search_parameters.__contains__('display_rarity'):
            parameters['displayRarity'] = search_parameters['display_rarity']
        if search_parameters.__contains__('backend_rarity'):
            parameters['backendRarity'] = search_parameters['backend_rarity']
        if search_parameters.__contains__('name'):
            parameters['name'] = search_parameters['name']
        if search_parameters.__contains__('short_description'):
            parameters['shortDescription'] = search_parameters['short_description']
        if search_parameters.__contains__('description'):
            parameters['description'] = search_parameters['description']
        if search_parameters.__contains__('set'):
            parameters['set'] = search_parameters['set']
        if search_parameters.__contains__('set_text'):
            parameters['setText'] = search_parameters['setText']
        if search_parameters.__contains__('series'):
            parameters['series'] = search_parameters['series']
        if search_parameters.__contains__('has_small_icon'):
            parameters['hasSmallIcon'] = search_parameters['has_small_icon']
        if search_parameters.__contains__('has_icon'):
            parameters['hasIcon'] = search_parameters['has_icon']
        if search_parameters.__contains__('has_featured_image'):
            parameters['hasFeaturedImage'] = search_parameters['has_featured_image']
        if search_parameters.__contains__('has_background_image'):
            parameters['hasBackgroundImage'] = search_parameters['has_background_image']
        if search_parameters.__contains__('has_cover_art'):
            parameters['hasCoverArt'] = search_parameters['has_cover_art']
        if search_parameters.__contains__('has_decal'):
            parameters['hasDecal'] = search_parameters['has_decal']
        if search_parameters.__contains__('has_variants'):
            parameters['hasVariants'] = search_parameters['has_variants']
        if search_parameters.__contains__('has_gameplay_tags'):
            parameters['hasGameplayTags'] = search_parameters['has_gameplay_tags']
        if search_parameters.__contains__('gameplay_tag'):
            parameters['gameplayTag'] = search_parameters['gameplay_tag']
        return parameters

    def fetch_all(self, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = self._client.http.get('cosmetics/br', params=params)
        if data is None:
            return None
        return [BrCosmetic(item_data) for item_data in data['data']]

    def search_by_id(self, *cosmetic_id: str, language=GameLanguage.ENGLISH):
        cosmetic_ids = list(cosmetic_id)
        params = {'language': language.value}

        if len(cosmetic_ids) < 1:
            return None
        endpoint = 'cosmetics/br/search/ids'
        endpoint += '?id=' + cosmetic_ids[0]
        del cosmetic_ids[0]
        endpoint += '&id='.join(cosmetic_ids)
        data = self._client.http.get(endpoint, params=params)
        if data is None:
            return None
        return [BrCosmetic(item_data) for item_data in data['data']]

    def search_all(self, **search_parameters):
        data = self._client.http.get('/cosmetics/br/search/all',
                                     params=self._parse_search_parameter(**search_parameters))
        if data is None:
            return None
        return [BrCosmetic(item_data) for item_data in data['data']]

    def search_first(self, **search_parameters):
        data = self._client.http.get('/cosmetics/br/search',
                                     params=self._parse_search_parameter(**search_parameters))
        if data is None:
            return None
        return BrCosmetic(data['data'])


class AsyncCosmeticsEndpoints:

    def __init__(self, client):
        self._client = client

    def _parse_search_parameter(self, **search_parameters):
        parameters = {
            'language': search_parameters.get('language', GameLanguage.ENGLISH).value,
            'searchLanguage': search_parameters.get('search_language', GameLanguage.ENGLISH).value,
            'matchMethod': search_parameters.get('match_method', MatchMethod.FULL).value
        }
        if search_parameters.__contains__('type'):
            parameters['type'] = search_parameters['type']
        if search_parameters.__contains__('backend_type'):
            parameters['backendType'] = search_parameters['backend_type']
        if search_parameters.__contains__('rarity'):
            parameters['rarity'] = search_parameters['rarity']
        if search_parameters.__contains__('backend_rarity'):
            parameters['backendRarity'] = search_parameters['backend_rarity']
        if search_parameters.__contains__('name'):
            parameters['name'] = search_parameters['name']
        if search_parameters.__contains__('short_description'):
            parameters['shortDescription'] = search_parameters['short_description']
        if search_parameters.__contains__('description'):
            parameters['description'] = search_parameters['description']
        if search_parameters.__contains__('set'):
            parameters['set'] = search_parameters['set']
        if search_parameters.__contains__('series'):
            parameters['series'] = search_parameters['series']
        if search_parameters.__contains__('has_small_icon'):
            parameters['hasSmallIcon'] = search_parameters['has_small_icon']
        if search_parameters.__contains__('has_icon'):
            parameters['hasIcon'] = search_parameters['has_icon']
        if search_parameters.__contains__('has_featured_image'):
            parameters['hasFeaturedImage'] = search_parameters['has_featured_image']
        if search_parameters.__contains__('has_background_image'):
            parameters['hasBackgroundImage'] = search_parameters['has_background_image']
        if search_parameters.__contains__('has_cover_art'):
            parameters['hasCoverArt'] = search_parameters['has_cover_art']
        if search_parameters.__contains__('has_decal'):
            parameters['hasDecal'] = search_parameters['has_decal']
        if search_parameters.__contains__('has_variants'):
            parameters['hasVariants'] = search_parameters['has_variants']
        if search_parameters.__contains__('has_gameplay_tags'):
            parameters['hasGameplayTags'] = search_parameters['has_gameplay_tags']
        if search_parameters.__contains__('gameplay_tag'):
            parameters['gameplayTag'] = search_parameters['gameplay_tag']
        return parameters

    async def fetch_all(self, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = await self._client.http.get('cosmetics/br', params=params)
        if data is None:
            return None
        return [BrCosmetic(item_data) for item_data in data['data']]

    async def search_by_id(self, *cosmetic_id: str, language=GameLanguage.ENGLISH):
        cosmetic_ids = list(cosmetic_id)
        params = {'language': language.value}

        if len(cosmetic_ids) < 1:
            return None
        endpoint = 'cosmetics/br/search/ids'
        endpoint += '?id=' + cosmetic_ids[0]
        del cosmetic_ids[0]
        endpoint += '&id='.join(cosmetic_ids)
        data = await self._client.http.get(endpoint, params=params)
        if data is None:
            return None
        return [BrCosmetic(item_data) for item_data in data['data']]

    async def search_all(self, **search_parameters):
        data = await self._client.http.get('/cosmetics/br/search/all',
                                           params=self._parse_search_parameter(**search_parameters))
        if data is None:
            return None
        return [BrCosmetic(item_data) for item_data in data['data']]

    async def search_first(self, **search_parameters):
        data = await self._client.http.get('/cosmetics/br/search',
                                           params=self._parse_search_parameter(**search_parameters))
        if data is None:
            return None
        return BrCosmetic(data['data'])


class SyncNewsEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch(self, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = self._client.http.get('news', params=params)
        if data is None:
            return None
        return News(data['data'])

    def fetch_by_type(self, news_type: NewsType, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = self._client.http.get('news/' + news_type.value, params=params)
        if data is None:
            return None
        return GameModeNews(data['data'])


class AsyncNewsEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch_news(self, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = await self._client.http.get('news', params=params)
        if data is None:
            return None
        return News(data['data'])

    async def fetch_by_type(self, news_type: NewsType, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = await self._client.http.get('news/' + news_type.value, params=params)
        if data is None:
            return None
        return GameModeNews(data['data'])


class SyncShopEndpoints:

    def __init__(self, client):
        self._client = client

    def fetch(self, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = self._client.http.get('shop/br', params=params)
        if data is None:
            return None
        return BrShop(data['data'])


class AsyncShopEndpoints:

    def __init__(self, client):
        self._client = client

    async def fetch(self, language=GameLanguage.ENGLISH):
        params = {'language': language.value}
        data = await self._client.http.get('shop/br', params=params)
        if data is None:
            return None
        return BrShop(data['data'])
