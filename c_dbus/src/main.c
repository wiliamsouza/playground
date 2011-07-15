#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <inttypes.h>
#include <dbus/dbus.h>

#include "macro.h"

struct unit_info {
        const char *id;
        const char *description;
        const char *load_state;
        const char *active_state;
        const char *sub_state;
        const char *following;
        const char *unit_path;
        uint32_t job_id;
        const char *job_type;
        const char *job_path;
};

int main(int argc, char* argv[]) {
        DBusConnection *bus = NULL;
        DBusMessage *message = NULL;
        DBusMessage *reply = NULL;
        DBusMessageIter iter, sub, sub2;
        DBusError error;
        unsigned c = 0, n_units = 0;
        struct unit_info *unit_infos = NULL;
        int r;
  
        dbus_error_init(&error);

        bus = dbus_bus_get(DBUS_BUS_SYSTEM, &error);

        if (!bus) {
                fprintf(stderr, "Failed to connect to dbus %s\n", error.message);
                dbus_error_free(&error);
                return -EIO;
        }

        message = dbus_message_new_method_call(
                                "org.freedesktop.systemd1",
                                "/org/freedesktop/systemd1",
                                "org.freedesktop.systemd1.Manager",
                                "ListUnits");

        if (!message) {
                fprintf(stderr, "Could not allocate message.");
                return -ENOMEM;
        }

        reply = dbus_connection_send_with_reply_and_block(bus, message, -1, &error);

        if (!reply) {
                fprintf(stderr, "Failed to issue method call.");
                dbus_error_free(&error);
                return -EIO;
        }


        if (!dbus_message_iter_init(reply, &iter) ||
            dbus_message_iter_get_arg_type(&iter) != DBUS_TYPE_ARRAY ||
            dbus_message_iter_get_element_type(&iter) != DBUS_TYPE_STRUCT) {
                fprintf(stderr, "Failed to parse reply.");
                dbus_error_free(&error);
                return -EIO;
        }

        // Walk forward to struct part of reply message
        dbus_message_iter_recurse(&iter, &sub);

        // the last item always will be a dbus invalid type
        while (dbus_message_iter_get_arg_type(&sub) != DBUS_TYPE_INVALID) {
                struct unit_info *u;

                // check if the type is what we want
                if (dbus_message_iter_get_arg_type(&sub) != DBUS_TYPE_STRUCT) {
                        fprintf(stderr, "Failed to parse reply.");
                        dbus_error_free(&error);
                        return -EIO;
                }

                if (c >= n_units) {
                        struct unit_info *w;

                        n_units = MAX(2*c, 16);
                        w = realloc(unit_infos, sizeof(struct unit_info) * n_units);

                        if (!w) {
                                fprintf(stderr, "Failed to allocate unit array.");
                                dbus_error_free(&error);
                                return -ENOMEM;
                        }

                        unit_infos = w;
                }

                u = unit_infos+c;

                dbus_message_iter_recurse(&sub, &sub2);

                //TODO: map message data do unit_info struct hehe!

                dbus_message_iter_next(&sub);
                c++;
        }

        if (c > 0) {
                printf("Print units here!\n");
        }

        return EXIT_SUCCESS;
}
