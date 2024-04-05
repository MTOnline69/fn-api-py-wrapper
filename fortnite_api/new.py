"""
MIT License

Copyright (c) 2019-present Luc1412

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

import datetime
from typing import Any, Dict, Generic, List, Optional, Type

from .cosmetics import CosmeticBr, CosmeticCar, CosmeticInstrument, CosmeticLego, CosmeticLegoKit, CosmeticT, CosmeticTrack
from .enums import CosmeticType
from .http import HTTPClientT
from .utils import parse_time


class NewCosmetic(Generic[CosmeticT]):
    """Represents a response from the new cosmetics endpoint for a given cosmetic type. The types are as follows:

    - ``CosmeticType.BR`` -> List of :class:`CosmeticBr`
    - ``CosmeticType.TRACKS`` -> List of :class:`CosmeticTrack`
    - ``CosmeticType.INSTRUMENTS`` -> List of :class:`CosmeticInstrument`
    - ``CosmeticType.CARS`` -> List of :class:`CosmeticCar`
    - ``CosmeticType.LEGO`` -> List of :class:`CosmeticLego`
    - ``CosmeticType.LEGO_KITS`` -> List of :class:`CosmeticLegoKit`

    Attributes
    ----------
    type: :class:`CosmeticType`
        The type of new cosmetics displayed.
    hash: Optional[:class:`str`]
        The hash of the new cosmetics. Can be ``None`` if no
        new cosmetics have been given for the cosmetic type.
    last_addition: :class:`datetime.datetime`
        The last addition of new cosmetics.
    items: List[:class:`BrCosmetic`]
        The new cosmetics. This corresponds to the type of new cosmetics.
        Can be empty if no new cosmetics have been given.
    """

    def __init__(
        self,
        *,
        type: CosmeticType,
        hash: Optional[str] = None,
        last_addition: Optional[datetime.datetime] = None,
        items: List[CosmeticT],
        http: HTTPClientT,
    ) -> None:
        self._http: HTTPClientT = http

        self.type: CosmeticType = type
        self.hash: Optional[str] = hash
        self.last_addition: Optional[datetime.datetime] = last_addition
        self.items: List[CosmeticT] = items


class NewBrCosmetics(NewCosmetic[CosmeticBr[HTTPClientT]]):
    """Represents a returned response from the new BR cosmetics endpoint.

    This inherits from :class:`NewCosmetic`.

    Attributes
    ----------
    build: :class:`str`
        The build of Fortnite that these cosmetics were added in.
    previous_build: :class:`str`
        The previous build of Fortnite.
    date: :class:`datetime.datetime`
        The date of the new cosmetics.
    raw_data: Dict[:class:`str`, Any]
        The raw data of the new cosmetics.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        items: List[CosmeticBr[HTTPClientT]] = [CosmeticBr(data=item, http=http) for item in data['items']]

        super().__init__(
            type=CosmeticType.BR,
            hash=data['hash'],
            last_addition=parse_time(data['lastAddition']),
            items=items,
            http=http,
        )

        # Extend this for the endpoint specific data
        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        self.date: datetime.datetime = parse_time(data['date'])
        self.raw_data: Dict[str, Any] = data


class NewCosmetics(Generic[HTTPClientT]):
    """Represents a response from the new cosmetics endpoint.

    Attributes
    ----------
    build: :class:`str`
        The build of Fortnite that these cosmetics were added in.
    previous_build: :class:`str`
        The previous build of Fortnite.
    date: :class:`datetime.datetime`
        The date of the new cosmetics.
    global_hash: :class:`str`
        The combined hash of all new cosmetics.
    global_last_addition: :class:`datetime.datetime`
        The last time a new cosmetic was added.
    br: :class:`NewCosmetic`
        The new BR cosmetics.
    tracks: :class:`NewCosmetic`
        The new track cosmetics.
    instruments: :class:`NewCosmetic`
        The new instrument cosmetics.
    cars: :class:`NewCosmetic`
        The new car cosmetics.
    lego: :class:`NewCosmetic`
        The new lego cosmetics.
    lego_kits: :class:`NewCosmetic`
        The new lego kit cosmetics.
    """

    def __init__(self, *, data: Dict[str, Any], http: HTTPClientT) -> None:
        self._http: HTTPClientT = http

        self.build: str = data['build']
        self.previous_build: str = data['previousBuild']
        self.date: datetime.datetime = parse_time(data['date'])
        self.global_hash: str = data['hashes']['all']
        self.global_last_addition: datetime.datetime = parse_time(data['lastAdditions']['all'])
        self.raw_data: Dict[str, Any] = data

        self.br: NewCosmetic[CosmeticBr[HTTPClientT]] = self._create_new_cosmetic(
            cosmetic_type=CosmeticType.BR,
            internal_key='br',
            cosmetic_class=CosmeticBr,
        )

        self.tracks: NewCosmetic[CosmeticTrack[HTTPClientT]] = self._create_new_cosmetic(
            cosmetic_type=CosmeticType.TRACKS,
            internal_key='tracks',
            cosmetic_class=CosmeticTrack,
        )

        self.instruments: NewCosmetic[CosmeticInstrument[HTTPClientT]] = self._create_new_cosmetic(
            cosmetic_type=CosmeticType.INSTRUMENTS,
            internal_key='instruments',
            cosmetic_class=CosmeticInstrument,
        )

        self.cars: NewCosmetic[CosmeticCar[HTTPClientT]] = self._create_new_cosmetic(
            cosmetic_type=CosmeticType.CARS,
            internal_key='cars',
            cosmetic_class=CosmeticCar,
        )

        self.lego: NewCosmetic[CosmeticLego[HTTPClientT]] = self._create_new_cosmetic(
            cosmetic_type=CosmeticType.LEGO,
            internal_key='lego',
            cosmetic_class=CosmeticLego,
        )

        self.lego_kits: NewCosmetic[CosmeticLegoKit[HTTPClientT]] = self._create_new_cosmetic(
            cosmetic_type=CosmeticType.LEGO_KITS,
            internal_key='legoKits',
            cosmetic_class=CosmeticLegoKit,
        )

    def _create_new_cosmetic(
        self,
        *,
        cosmetic_type: CosmeticType,
        internal_key: str,
        cosmetic_class: Type[CosmeticT],
    ) -> NewCosmetic[CosmeticT]:
        hashes = self.raw_data['hashes']
        last_additions = self.raw_data['lastAdditions']
        items = self.raw_data['items']

        cosmetic_items: List[Dict[str, Any]] = items[internal_key] or []

        last_addition_str = last_additions[internal_key]
        last_addition: Optional[datetime.datetime] = parse_time(last_addition_str) if last_addition_str else None

        return NewCosmetic(
            type=cosmetic_type,
            hash=hashes[internal_key],
            last_addition=last_addition,
            items=[cosmetic_class(data=item, http=self._http) for item in cosmetic_items],
            http=self._http,
        )
