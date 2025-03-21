import os
import platform

import spack.compilers
from spack.package import *

_sha = '748a9ce395b962cef1eef6e761b2b37a4f817b403ddab61ea53387890bdc5041'

_versions = {
    "1.0": {
        "Linux-aarch64": _sha,
        "Linux-x86_64": _sha,
    },
}


class Hello(MakefilePackage):
    """hello"""

    homepage = "https://www.cscs.ch"
    url = "https://jfrog.svc.cscs.ch/artifactory/cscs-reframe-tests/hello/hello-1.0.tar.gz"
    maintainers = ["jgphpc"]

    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        sha = packages.get(key)
        if sha:
            version(
                ver,
                sha256=sha,
                preferred=(ver == "1.0"),
                url=f"https://jfrog.svc.cscs.ch/artifactory/cscs-reframe-tests/hello/hello-{ver}.tar.gz"
            )

    variant("cuda", default=False)

    conflicts("%gcc@:7")

    depends_on("c", type="build")
    depends_on("cuda", when="+cuda")

    def build(self, spec, prefix):
        if "+cuda" in spec:
            make("-f", "Makefile", "gpu")
        else:
            make("-f", "Makefile", "cpu")

    def install(self, spec, prefix):
        if "+cuda" in spec:
            make("-f", "Makefile", f"prefix={prefix}", "install_gpu")
        else:
            make("-f", "Makefile", f"prefix={prefix}", "install_cpu")
