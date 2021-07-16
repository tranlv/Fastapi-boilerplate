#!/usr/bin/env python
# -*- coding: utf-8 -*-

# third-party modules
from flask_restx import Resource

# own modules
from app.modules.sample_mod.sample_controller import SampleController
from app.modules.sample_mod.sample_dto import SampleDto
from app.extensions.utils.decorator import token_required


__author__ = "hoovada.com team"
__maintainer__ = "hoovada.com team"
__email__ = "admin@hoovada.com"
__copyright__ = "Copyright (c) 2020 - 2020 hoovada.com . All Rights Reserved."


api = SampleDto.api

@api.route('', methods=['POST'])
class Sample(Resource):
    @token_required
    @api.expect()
    @api.response()
    def post(self):
        return SampleController().create(api.payload)
