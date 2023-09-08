import io
import json
import logging

from werkzeug.datastructures import FileStorage

from odoo import http
from odoo.http import request

from odoo.addons.g2p_self_service_portal.controllers.main import SelfServiceController

_logger = logging.getLogger(__name__)


class FormioStorageFilestoreController(http.Controller):
    @http.route("/storage/s3", type="json", auth="public", method=["POST"], csrf=False)
    def storage_in_s3(self, **post):

        data = json.loads(http.request.httprequest.data)

        process_data = self.create_file_storage(
            data
        )  # converting into filestorage object
        program = request.env["g2p.program"].browse(1)
        SelfServiceController.add_file_to_store(
            process_data,
            store=program.supporting_documents_store,
            program_membership=None,
            tags=None,
        )

    def create_file_storage(self, data):
        filename = data.get("name", "default_filename.txt")
        content = data.get("content", b"")

        file_storage = FileStorage(
            stream=io.BytesIO(content),
            filename=filename,
            content_type=data.type,
        )

        return file_storage
