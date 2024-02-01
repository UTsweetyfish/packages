
from os import mkdir
from jinja2 import Environment, PackageLoader
from jinja2 import select_autoescape

from debian.debian_support import version_compare

from .download import prepare

if __name__ == '__main__':

    env = Environment(
        loader=PackageLoader('packages'),
        autoescape=select_autoescape(),
    )
    env.globals.update(version_compare=version_compare)
    tmpl = env.get_template('index.html')

    raw_data = prepare()

    mkdir('output')

    with open('output/index.html', 'w', encoding='utf-8') as f:
        f.write(tmpl.render({
            'packages': raw_data,
            'distros': ['beige', 'sid'],
        }))
    
    ESSENTIAL = 'acl apt attr audit base-files base-passwd bash binutils build-essential bzip2 cdebconf coreutils dash db5.3 debianutils diffutils dpkg dwz e2fsprogs elfutils elogind file findutils gawk gcc-13 gcc-defaults gdbm gettext glibc gmp gnupg2 gnutls28 grep groff guile-3.0 gzip hostname icu isl jansson keyutils krb5 libcap-ng libcap2 libffi libgc libgcrypt20 libgpg-error libidn2 libmd libnsl libpipeline libseccomp libselinux libsigsegv libtasn1-6 libtirpc libunistring libxcrypt libxml2 libzstd lz4 m4 make-dfsg man-db mpclib3 mpfr4 ncurses nettle openssl p11-kit pam patch pcre2 perl readline rpcsvc-proto sed shadow systemd sysvinit tar uchardet util-linux xxhash xz-utils zlib'.split()
    
    with open('output/index-essential.html', 'w', encoding='utf-8') as f:
        f.write(tmpl.render({
            'packages': {k: v for k, v in raw_data.items() if k in ESSENTIAL},
            'distros': ['beige', 'sid'],
        }))