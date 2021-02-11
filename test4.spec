import com.atlassian.bamboo.specs.api.BambooSpec;
import com.atlassian.bamboo.specs.api.builders.BambooKey;
import com.atlassian.bamboo.specs.api.builders.BambooOid;
import com.atlassian.bamboo.specs.api.builders.permission.PermissionType;
import com.atlassian.bamboo.specs.api.builders.permission.Permissions;
import com.atlassian.bamboo.specs.api.builders.permission.PlanPermissions;
import com.atlassian.bamboo.specs.api.builders.plan.Job;
import com.atlassian.bamboo.specs.api.builders.plan.Plan;
import com.atlassian.bamboo.specs.api.builders.plan.PlanIdentifier;
import com.atlassian.bamboo.specs.api.builders.plan.Stage;
import com.atlassian.bamboo.specs.api.builders.plan.branches.BranchCleanup;
import com.atlassian.bamboo.specs.api.builders.plan.branches.PlanBranchManagement;
import com.atlassian.bamboo.specs.api.builders.plan.configuration.ConcurrentBuilds;
import com.atlassian.bamboo.specs.api.builders.project.Project;
import com.atlassian.bamboo.specs.api.builders.requirement.Requirement;
import com.atlassian.bamboo.specs.builders.task.ScriptTask;
import com.atlassian.bamboo.specs.util.BambooServer;

@BambooSpec
public class PlanSpec {
    
    public Plan plan() {
        final Plan plan = new Plan(new Project()
                .oid(new BambooOid("zld3n2j43g1v"))
                .key(new BambooKey("SPEC"))
                .name("SPEC")
                .description("SPECS Testing"),
            "TEST4",
            new BambooKey("TEST4"))
            .oid(new BambooOid("zl3efh5w9ogd"))
            .description("SPEC test plan 4")
            .pluginConfigurations(new ConcurrentBuilds())
            .stages(new Stage("Default Stage")
                    .jobs(new Job("Default Job",
                            new BambooKey("JOB1"))
                            .tasks(new ScriptTask()
                                    .description("script test")
                                    .inlineBody("#!/usr/bin/env python3\n\\n\nimport sys\n\\n\ndef main():\nprint(\"it is alive.\")\nsys.exit(0)\n\\n\nif __name__ == \"__main__\":\nmain()"))
                            .requirements(new Requirement("spec_test")
                                    .matchValue("1")
                                    .matchType(Requirement.MatchType.EQUALS))))
            .planBranchManagement(new PlanBranchManagement()
                    .delete(new BranchCleanup())
                    .notificationForCommitters()
                    .issueLinkingEnabled(false));
        return plan;
    }
    
    public PlanPermissions planPermission() {
        final PlanPermissions planPermission = new PlanPermissions(new PlanIdentifier("SPEC", "TEST4"))
            .permissions(new Permissions()
                    .userPermissions("dschweizer", PermissionType.EDIT, PermissionType.VIEW, PermissionType.ADMIN, PermissionType.CLONE, PermissionType.BUILD));
        return planPermission;
    }
    
    public static void main(String... argv) {
        //By default credentials are read from the '.credentials' file.
        BambooServer bambooServer = new BambooServer("https://ci2.netdef.org");
        final PlanSpec planSpec = new PlanSpec();
        
        final Plan plan = planSpec.plan();
        bambooServer.publish(plan);
        
        final PlanPermissions planPermission = planSpec.planPermission();
        bambooServer.publish(planPermission);
    }
}
