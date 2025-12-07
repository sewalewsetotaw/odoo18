/** @odoo-module **/
import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

const actionRegistry = registry.category("actions");

class SchoolDashboard extends Component {
    setup() {
        super.setup();
        this.orm = useService("orm");
        this._fetch_data();
    }

    async _fetch_data() {
        const result = await this.orm.call("school.dashboard", "get_dashboard_data", [], {});

        document.getElementById("total_students").innerHTML = `<span>${result.students}</span>`;
        document.getElementById("total_enrollments").innerHTML = `<span>${result.enrollments}</span>`;
        document.getElementById("total_fees").innerHTML = `<span>${result.fees}</span>`;
        document.getElementById("total_attendance").innerHTML = `<span>${result.attendance}</span>`;
        document.getElementById("total_courses").innerHTML = `<span>${result.courses}</span>`;
        document.getElementById("total_teachers").innerHTML = `<span>${result.teachers}</span>`;
        document.getElementById("total_sections").innerHTML = `<span>${result.sections}</span>`;
        document.getElementById("total_exams").innerHTML = `<span>${result.exams}</span>`;
    }
}

SchoolDashboard.template = "school_management.SchoolDashboard";
actionRegistry.add("school_dashboard_tag", SchoolDashboard);
